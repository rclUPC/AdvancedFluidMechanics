/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Description
    Template for use with codeStream.

\*---------------------------------------------------------------------------*/

#include "dictionary.H"
#include "fieldTypes.H"
#include "Ostream.H"
#include "Pstream.H"
#include "read.H"
#include "unitConversion.H"

//{{{ begin codeInclude

//}}} end codeInclude

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    void codeStream_e56ebce62bd85a7c2e03fa22992668037d40a988
    (
        Ostream& os,
        const dictionary& dict
    )
    {
//{{{ begin code
        #line 178 "/home/robert/GDriveUPC/Documents/asignaturas/AdvancedFluidMechanics/JupyterNotebooks/3-Turbulence/OF11/rotor2D/system/blockMeshDict/#codeStream"
const label viN = 4*dict.lookupScoped<label>("nBlades", true, false);

                    auto makeFace = [&](const label v0, const label v1)
                    {
                        os  << labelList({v0%viN, v1%viN, v1%viN+viN, v0%viN+viN});
                    };

                    for (label i = 0; i < dict.lookupScoped<label>("nBlades", true, false); i ++)
                    {
                        const label vi0 = i*4;
                        makeFace(vi0+2, vi0+1);
                        makeFace(vi0+1, vi0+4);
                        makeFace(vi0+4, vi0+6);
                    }
//}}} end code
    }
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

